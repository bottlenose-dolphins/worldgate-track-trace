resource "aws_service_discovery_private_dns_namespace" "tracktrace" {
  name        = "tracktrace"
  description = "Devlopment environment web"
  vpc         = aws_default_vpc.default_vpc.id
  
}

resource "aws_service_discovery_service" "frontend" {
  name = "frontend"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}

resource "aws_service_discovery_service" "core_user" {
  name = "core_user"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}

resource "aws_service_discovery_service" "scraper_ymlu" {
  name = "scraper_ymlu"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}

resource "aws_service_discovery_service" "scraper_kmtc" {
  name = "scraper_kmtc"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}

resource "aws_service_discovery_service" "scraper_good" {
  name = "scraper_good"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}

resource "aws_service_discovery_service" "scraper_one" {
  name = "scraper_one"
  dns_config {
    namespace_id = "${aws_service_discovery_private_dns_namespace.tracktrace.id}"

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 5
  }
}