resource "aws_cloudwatch_log_group" "tracktrace_core_load_bl_doc_log" {
    name = "tracktrace_core_load_bl_doc_log"
}

resource "aws_ecs_task_definition" "tracktrace_core_load_bl_doc" {
    family                   = "tracktrace_core_load_bl_doc" 
    container_definitions    = <<DEFINITION
    [
        {
        "name": "tracktrace_core_load_bl_doc",
        "image": "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:core_load-bl-doc",
        "essential": true,
        "portMappings": [
            {
            "containerPort": 5014,
            "hostPort": 5014
            }
        ],
        "memory": 512,
        "cpu": 256,
        "runtimePlatform": {
        "operatingSystemFamily": "LINUX",
        "cpuArchitecture": "ARM64"
        },
        "overrides": { 
            "taskRoleArn": "arn:aws:iam::283879969377:role/load_bl_doc_role"
        },
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "tracktrace_core_load_bl_doc_log",
            "awslogs-region": "ap-southeast-1",
            "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
    DEFINITION
    runtime_platform {
        cpu_architecture = "ARM64"
        operating_system_family = "LINUX"
    }
    task_role_arn         = "arn:aws:iam::283879969377:role/load_bl_doc_role"
    requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
    network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
    memory                   = 512         # Specifying the memory our container requires
    cpu                      = 256         # Specifying the CPU our container requires
    execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole2.arn}"
}

resource "aws_ecs_service" "tracktrace_core_load_bl_doc_service" {
    name            = "tracktrace_core_load_bl_doc_service"                             # Naming our first service
    cluster         = "${aws_ecs_cluster.tracktrace_cluster.id}"             # Referencing our created Cluster
    task_definition = "${aws_ecs_task_definition.tracktrace_core_load_bl_doc.arn}" # Referencing the task our service will spin up
    launch_type     = "FARGATE"
    desired_count   = 1 # Setting the number of containers we want deployed to 2

    network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}", "${aws_default_subnet.default_subnet_c.id}"]
    assign_public_ip = true # Providing our containers with public IPs
    }

    load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group_core_load_bl_doc.arn}" # Referencing our target group
    container_name   = "${aws_ecs_task_definition.tracktrace_core_load_bl_doc.family}"
    container_port   = 5014 # Specifying the container port
    }

    service_registries {
    registry_arn = "${aws_service_discovery_service.core_load_bl_doc.arn}"
    }
}

resource "aws_lb_target_group" "target_group_core_load_bl_doc" {
    name        = "tg-core-load-bl-doc"
    port        = 5014
    protocol    = "HTTP"
    target_type = "ip"
    vpc_id      = "${aws_default_vpc.default_vpc.id}" # Referencing the default VPC
    health_check {
        matcher = "200,301,302"
        path = "/ping"
    }

    lifecycle {
        create_before_destroy = false
    }
}

resource "aws_lb_listener" "listener_core_load_bl_doc" {
    load_balancer_arn = "${aws_alb.internal_load_balancer.arn}" # Referencing our load balancer
    port              = "5014"
    protocol          = "HTTP"
    default_action {
        type             = "forward"
        target_group_arn = "${aws_lb_target_group.target_group_core_load_bl_doc.arn}" # Referencing our tagrte group
    }
}