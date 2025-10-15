resource "aws_ecr_repository" "app" {
  name                 = "${local.project}-${local.env}"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = local.tags
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

