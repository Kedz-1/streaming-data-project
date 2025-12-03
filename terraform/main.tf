resource "aws_sqs_queue" "guardian_queue" {
  name = "guardian_queue"
  
  tags = {
    Environment = "GuardianAPI"
  }
}
