resource "aws_instance" "my_server" {

  ami           = "ami-06067086cf86c58e6"
  instance_type = "t3.micro"

  tags = {
    Name = "Terraform-Server"
  }
}
