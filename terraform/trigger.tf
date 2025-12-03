resource "aws_cloudwatch_event_rule" "lambda_trigger" {
  name_prefix        = "sqs_guardian_update"
  description = "Send Guardian top articles every 12 hours"
  
  schedule_expression = "rate(12 hours)"
  
}

resource "aws_cloudwatch_event_target" "invoke_lambda" {
  rule      = aws_cloudwatch_event_rule.lambda_trigger.name
  arn = aws_lambda_function.sqs_lambda.arn
}