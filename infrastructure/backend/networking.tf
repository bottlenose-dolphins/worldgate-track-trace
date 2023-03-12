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

resource "aws_security_group" "load_balancer_sec_group_default" {
    name        = "load_balancer_security_group"
    description = "Only our IPs"

    ingress {
        from_port   = 0 # Allowing any incoming port
        to_port     = 0 # Allowing any outgoing port
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"] # Allowing traffic in from all sources
    }

    egress {
        from_port   = 0 # Allowing any incoming port
        to_port     = 0 # Allowing any outgoing port
        protocol    = "-1" # Allowing any outgoing protocol 
        cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
    }
}

# #Internal load balancer

resource "aws_alb" "internal_load_balancer" {
    name               = "int-load-balancer" # Naming our load balancer
    load_balancer_type = "application"
    subnets = [ # Referencing the default subnets
        "${aws_default_subnet.default_subnet_a.id}",
        "${aws_default_subnet.default_subnet_b.id}",
        "${aws_default_subnet.default_subnet_c.id}"
    ]
security_groups = ["${aws_security_group.load_balancer_default_security_group.id}"]
}

# Security group for internal load balancer
resource "aws_security_group" "load_balancer_default_security_group" {
    ingress {
        from_port   = 0 
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"] # Allowing traffic in from all sources
    }

    egress {
        from_port   = 0 # Allowing any incoming port
        to_port     = 0 # Allowing any outgoing port
        protocol    = "-1" # Allowing any outgoing protocol 
        cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
    }
}
