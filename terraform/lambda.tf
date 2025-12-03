
resource "aws_lambda_function" "sqs_lambda" {
  function_name    = "guardian_lambda_function"
  role             = aws_iam_role.iam_role.arn

  filename = "../lambda_function.zip"

  environment {
    variables = {
      SEARCH_TERM = "and"
      QUEUE_NAME = aws_sqs_queue.guardian_queue.name
      DATE_FROM   = "2025-11-01"
      GUARDIAN_KEY = "e9fb40b6-70ab-4796-84a2-d8bc8d550c3e"
    
    }
  }

  handler = "handler.handler"
  runtime = "python3.11"
  tags = {
    Environment = "production"
    Application = "Lambda for automated Guardian to SQS messages"
  }

}
