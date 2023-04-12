#for resources already created in the backend terraform scripts

#ecs
data "aws_iam_role" "ecsTaskExecutionRole2" {
    name               = "ecsTaskExecutionRole2"
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
    role       = "${data.aws_iam_role.ecsTaskExecutionRole2.name}"
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_ecs_cluster" "tracktrace_cluster" {
    cluster_name = "tracktrace_cluster" # Naming the cluster
}

data "aws_alb" "int_load_balancer" {
  name = "int-load-balancer"
}



#networking
resource "aws_default_vpc" "default_vpc" {
    enable_dns_support   = true
    enable_dns_hostnames = true
}

resource "aws_default_subnet" "default_subnet_a" {
    availability_zone = "ap-southeast-1a"
}

resource "aws_default_subnet" "default_subnet_b" {
    availability_zone = "ap-southeast-1b"
}

resource "aws_default_subnet" "default_subnet_c" {
    availability_zone = "ap-southeast-1c"
}



