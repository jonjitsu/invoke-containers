
resource "random_id" "id" {
  prefix = "id-"
  byte_length = 8
}

output "id" {
  value = random_id.id.hex
}