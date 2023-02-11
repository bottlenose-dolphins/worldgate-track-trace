resource "aws_ecs_service" "tracktrace_default_subnet_fe_service" {
    name            = "tracktrace_default_subnet_fe_service"                             # Naming our first service
    cluster         = "${aws_ecs_cluster.tracktrace_cluster.id}"             # Referencing our created Cluster
    task_definition = "${aws_ecs_task_definition.tracktrace_test_task2.arn}" # Referencing the task our service will spin up
    launch_type     = "FARGATE"
    desired_count   = 2 # Setting the number of containers we want deployed to 2

    load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group_fe_default_subnet.arn}" # Referencing our target group
    container_name   = "${aws_ecs_task_definition.tracktrace_test_task2.family}"
    container_port   = 3000 # Specifying the container port
    }

    network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}", "${aws_default_subnet.default_subnet_c.id}"]
    assign_public_ip = true # Providing our containers with public IPs
    }

    service_registries {
    registry_arn = "${aws_service_discovery_service.frontend.arn}"
    }
}

resource "aws_ecs_task_definition" "tracktrace_test_task2" {
    family                   = "tracktrace_test_task2" # Naming our first task
    container_definitions    = <<DEFINITION
    [
        {
        "name": "tracktrace_test_task2",
        "image": "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:frontend_v1.0_ARM",
        "essential": true,
        "portMappings": [
            {
            "containerPort": 3000,
            "hostPort": 3000
            }
        ],
        "memory": 1024,
        "cpu": 512,
        "runtimePlatform": {
        "operatingSystemFamily": "LINUX",
        "cpuArchitecture": "ARM64"
        },
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "tracktrace_fe",
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
    requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
    network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
    memory                   = 1024         # Specifying the memory our container requires
    cpu                      = 512         # Specifying the CPU our container requires
    execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole2.arn}"
}


resource "aws_cloudwatch_log_group" "tracktrace_fe" {
  name = "tracktrace_fe"
}
