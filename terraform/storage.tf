resource "aws_s3_bucket" "static_media" {
  bucket = "${local.project}-${local.env}-assets"
  tags   = local.tags
}

