provider "aws" {
  region = "us-east-2" 
}

# Dynamically look up the official Ubuntu 24.04 image to prevent string errors
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}

# Create the custom network space for AnLog
resource "aws_vpc" "anlog_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "AnLog-VPC"
  }
}

# Create a public subnet inside the AnLog network
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.anlog_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-2a"
  map_public_ip_on_launch = true 

  tags = {
    Name = "AnLog-PublicSubnet"
  }
}
# Generates a secure SSH key pair automatically
resource "aws_key_pair" "anlog_ssh_key" {
  key_name   = "anlog-admin-key"
  public_key = file("~/.ssh/id_ed25519.pub") 
}

# Launch the core AnLog application server inside your custom subnet
resource "aws_instance" "anlog_app_server" {
  ami           = data.aws_ami.ubuntu.id # References the dynamic lookup above
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_subnet.id
key_name  = aws_key_pair.anlog_ssh_key.key_name
vpc_security_group_ids = [aws_security_group.anlog_fw.id]

  root_block_device {
    volume_size = 10
    volume_type = "gp3"
  }

  tags = {
    Name        = "AnLog-AppServer"
    Environment = "Dev"
    Project     = "AnLog-Core"
  }
}
resource "aws_security_group" "anlog_fw" {
  name        = "anlog-core-firewall"
  description = "Allow inbound SSH access"
  vpc_id      = aws_vpc.anlog_vpc.id

  # Inbound rules: Allow SSH (Port 22) from your IP address
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # In production, you'd limit this to your exact home IP
  }

  # Outbound rules: Allow the server to talk to the internet (to download updates)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# 1. Create an Internet Gateway so the VPC can talk to the outside world
resource "aws_internet_gateway" "anlog_igw" {
  vpc_id = aws_vpc.anlog_vpc.id

  tags = {
    Name = "AnLog-InternetGateway"
  }
}

# 2. Create a Route Table that routes all traffic (0.0.0.0/0) out through the Gateway
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.anlog_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.anlog_igw.id
  }

  tags = {
    Name = "AnLog-PublicRouteTable"
  }
}

# 3. Explicitly connect the Route Table to your public subnet
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}