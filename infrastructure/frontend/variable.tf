# route 53 variables
variable "domain_name" {
    default       = "worldgatetracktrace.click"
    description   = "domain name"
    type          = string
}

variable "record_name" {
    default       = "www"
    description   = "sub domain name"
    type          = string
}