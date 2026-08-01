variable "name" { type = string }
variable "cluster_name" { type = string }
variable "vpc_cidr" { type = string }
variable "availability_zones" {
  type    = number
  default = 3
}
variable "nat_gateway_per_az" {
  type    = bool
  default = true
}
variable "tags" {
  type    = map(string)
  default = {}
}
