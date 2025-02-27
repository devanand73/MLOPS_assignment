# EKS Cluster Security Group
resource "aws_security_group" "eks_cluster" {
  name        = "mlops-eks-cluster-sg"
  description = "Cluster communication"
  vpc_id      = aws_vpc.mlops_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Node Security Group
resource "aws_security_group" "eks_nodes" {
  name        = "mlops-eks-node-sg"
  description = "Security group for all nodes in the cluster"
  vpc_id      = aws_vpc.mlops_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.mlops_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}