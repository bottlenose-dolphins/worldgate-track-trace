output "REACT_APP_API_ENDPOINT" {
  description = "dns name for internal alb"
  value       = aws_alb.internal_load_balancer.dns_name
}

resource "local_file" "REACT_APP_API_ENDPOINT" {
    content  = aws_alb.internal_load_balancer.dns_name
    filename = "../../services/frontend/.env"
}

