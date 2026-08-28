terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}


# -------------------------
# VPC
# -------------------------

resource "aws_vpc" "cloudops" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "cloudops-vpc"
  }
}


# -------------------------
# Internet Gateway
# -------------------------

resource "aws_internet_gateway" "cloudops" {
  vpc_id = aws_vpc.cloudops.id

  tags = {
    Name = "cloudops-internet-gateway"
  }
}


# -------------------------
# Public Subnets
# -------------------------

resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.cloudops.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "cloudops-public-1"
  }
}


resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.cloudops.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "cloudops-public-2"
  }
}


# -------------------------
# Route Table
# -------------------------

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloudops.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cloudops.id
  }

  tags = {
    Name = "cloudops-public-route-table"
  }
}


# -------------------------
# Route Table Associations
# -------------------------

resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}


resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}