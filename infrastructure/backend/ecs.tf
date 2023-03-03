resource "aws_iam_role" "ecsTaskExecutionRole2" {
    name               = "ecsTaskExecutionRole2"
    assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
    statement {
        actions = ["sts:AssumeRole"]

        principals {
        type        = "Service"
        identifiers = ["ecs-tasks.amazonaws.com"]
        }
    }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
    role       = "${aws_iam_role.ecsTaskExecutionRole2.name}"
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


resource "aws_ecs_cluster" "tracktrace_cluster" {
    name = "tracktrace_cluster" # Naming the cluster
}