resource "aws_cloudwatch_log_group" "tracktrace_scraper_one" {
    name = "tracktrace_scraper_one"
}

resource "aws_ecs_task_definition" "tracktrace_scraper_one" {
    family                   = "tracktrace_scraper_one" 
    container_definitions    = <<DEFINITION
    [
        {
        "name": "tracktrace_scraper_one",
        "image": "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:scraper_One_v1.2_ARM",
        "essential": true,
        "portMappings": [
            {
            "containerPort": 80,
            "hostPort": 80
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
            "awslogs-group": "tracktrace_scraper_one",
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
    cpu                      = 512        # Specifying the CPU our container requires
    execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole2.arn}"
}


resource "aws_ecs_service" "tracktrace_scraper_one_service" {
    name            = "tracktrace_scraper_one_service"                             # Naming our first service
    cluster         = "${aws_ecs_cluster.tracktrace_cluster.id}"             # Referencing our created Cluster
    task_definition = "${aws_ecs_task_definition.tracktrace_scraper_one.arn}" # Referencing the task our service will spin up
    launch_type     = "FARGATE"
    desired_count   = 1 # Setting the number of containers we want deployed to 2

    network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}", "${aws_default_subnet.default_subnet_c.id}"]
    assign_public_ip = true # Providing our containers with public IPs
    }

    service_registries {
    registry_arn = "${aws_service_discovery_service.scraper_one.arn}"
    }
}
