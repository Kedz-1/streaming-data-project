resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEvent"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sqs_lambda.id
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_trigger.arn
}