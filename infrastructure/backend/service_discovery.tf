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

resource "aws_service_discovery_service" "scraper_cord" {
  name = "scraper_cord"
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

resource "aws_service_discovery_service" "scraper_cosco" {
  name = "scraper_cosco"
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

resource "aws_service_discovery_service" "core_import" {
  name = "core_import"
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

resource "aws_service_discovery_service" "core_import_cont" {
  name = "core_import_cont"
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

resource "aws_service_discovery_service" "core_import_shipment" {
  name = "core_import_shipment"
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

resource "aws_service_discovery_service" "core_export" {
  name = "core_export"
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

resource "aws_service_discovery_service" "core_export_cont" {
  name = "core_export_cont"
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



resource "aws_service_discovery_service" "core_export_shipment" {
  name = "core_export_shipment"
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

resource "aws_service_discovery_service" "core_prefix" {
  name = "core_prefix"
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

resource "aws_service_discovery_service" "core_view_all" {
  name = "core_view_all"
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

resource "aws_service_discovery_service" "core_vendor_mast" {
  name = "core_vendor_mast"
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

resource "aws_service_discovery_service" "core_complex_scraper" {
  name = "core_complex_scraper"
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