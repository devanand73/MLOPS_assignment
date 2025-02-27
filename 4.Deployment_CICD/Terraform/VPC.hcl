# VPC
resource "aws_vpc" "mlops_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "mlops-vpc"
  }
}

# Public Subnets (for load balancers)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.mlops_vpc.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "mlops-public-subnet-${count.index}"
  }
}

# Private Subnets (for EKS worker nodes)
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.mlops_vpc.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "mlops-private-subnet-${count.index}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.mlops_vpc.id
  tags = {
    Name = "mlops-igw"
  }
}

# NAT Gateway for private subnets
resource "aws_eip" "nat" {
  count = 2
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  tags = {
    Name = "mlops-nat-${count.index}"
  }
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.mlops_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}