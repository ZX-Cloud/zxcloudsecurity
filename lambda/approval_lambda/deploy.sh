#!/usr/bin/env bash
# deploy.sh
# ZX Cloud Security — Approval Lambda Deploy Script
#
# Packages handler.py into a ZIP and creates or updates the Lambda function.
# Run from the repo root or from lambda/approval_lambda/.
#
# Usage:
#   ./lambda/approval_lambda/deploy.sh
#
# Required environment variables (set as GitHub Actions secrets):
#   AWS_REGION            e.g. eu-west-2
#   LAMBDA_FUNCTION_NAME  e.g. zxcloudsecurity-approval
#   LAMBDA_ROLE_ARN       IAM role ARN for the Lambda execution role
#   DYNAMODB_TABLE        e.g. guide-approval-tokens
#   GITHUB_PAT_SECRET     Secrets Manager secret name (zxcloudsecurity/github-pat)
#   GITHUB_REPO           e.g. ZX-Cloud/zxcloudsecurity
#   SES_FROM_ADDRESS      Verified SES sender
#   SES_TO_ADDRESS        Steve's email

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(mktemp -d)"
ZIP_PATH="${BUILD_DIR}/approval_lambda.zip"

REGION="${AWS_REGION:-eu-west-2}"
FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-zxcloudsecurity-approval}"

echo "──────────────────────────────────────────"
echo "  ZX Cloud Security — Lambda Deploy"
echo "  Function: ${FUNCTION_NAME}"
echo "  Region:   ${REGION}"
echo "──────────────────────────────────────────"

# 1. Package handler.py into a ZIP
echo "[1/4] Packaging handler.py ..."
cp "${SCRIPT_DIR}/handler.py" "${BUILD_DIR}/handler.py"
(cd "${BUILD_DIR}" && zip -q "${ZIP_PATH}" handler.py)
echo "  → ${ZIP_PATH} ($(du -sh "${ZIP_PATH}" | cut -f1))"

# 2. Check whether function already exists
echo "[2/4] Checking if function exists ..."
if aws lambda get-function \
     --function-name "${FUNCTION_NAME}" \
     --region "${REGION}" \
     --query 'Configuration.FunctionName' \
     --output text 2>/dev/null | grep -q "${FUNCTION_NAME}"; then

  echo "  → Function exists — updating code ..."
  aws lambda update-function-code \
    --function-name "${FUNCTION_NAME}" \
    --zip-file "fileb://${ZIP_PATH}" \
    --region "${REGION}" \
    --query 'FunctionArn' \
    --output text

  # Wait for update to complete before configuring
  echo "  → Waiting for update to propagate ..."
  sleep 5

  echo "  → Updating environment variables ..."
  aws lambda update-function-configuration \
    --function-name "${FUNCTION_NAME}" \
    --region "${REGION}" \
    --environment "Variables={DYNAMODB_TABLE=${DYNAMODB_TABLE},GITHUB_REPO=${GITHUB_REPO},GITHUB_PAT_SECRET=${GITHUB_PAT_SECRET},SES_FROM_ADDRESS=${SES_FROM_ADDRESS},SES_TO_ADDRESS=${SES_TO_ADDRESS}}" \
    --query 'FunctionArn' \
    --output text

else
  echo "  → Function does not exist — creating ..."
  aws lambda create-function \
    --function-name "${FUNCTION_NAME}" \
    --runtime python3.12 \
    --role "${LAMBDA_ROLE_ARN}" \
    --handler handler.lambda_handler \
    --zip-file "fileb://${ZIP_PATH}" \
    --region "${REGION}" \
    --timeout 15 \
    --memory-size 128 \
    --environment "Variables={DYNAMODB_TABLE=${DYNAMODB_TABLE},GITHUB_REPO=${GITHUB_REPO},GITHUB_PAT_SECRET=${GITHUB_PAT_SECRET},SES_FROM_ADDRESS=${SES_FROM_ADDRESS},SES_TO_ADDRESS=${SES_TO_ADDRESS}}" \
    --query 'FunctionArn' \
    --output text

  echo "  → Waiting for function to become active ..."
  sleep 10

  # 3. Create Function URL (public HTTPS, no auth — secured by token)
  echo "[3/4] Creating Function URL ..."
  FUNCTION_URL=$(aws lambda create-function-url-config \
    --function-name "${FUNCTION_NAME}" \
    --auth-type NONE \
    --cors '{"AllowOrigins":["*"],"AllowMethods":["GET","POST"],"AllowHeaders":["content-type"]}' \
    --region "${REGION}" \
    --query 'FunctionUrl' \
    --output text)

  # Allow public invocation via Function URL
  aws lambda add-permission \
    --function-name "${FUNCTION_NAME}" \
    --statement-id FunctionURLAllowPublicAccess \
    --action lambda:InvokeFunctionUrl \
    --principal "*" \
    --function-url-auth-type NONE \
    --region "${REGION}" \
    --output text > /dev/null

  echo "  → Function URL: ${FUNCTION_URL}"
  echo ""
  echo "  ⚠ ACTION REQUIRED: Set APPROVAL_LAMBDA_URL in GitHub Actions secrets:"
  echo "    ${FUNCTION_URL%/}"
fi

# 4. Clean up
echo "[4/4] Cleaning up ..."
rm -rf "${BUILD_DIR}"

echo ""
echo "──────────────────────────────────────────"
echo "  Deploy complete ✓"
echo "──────────────────────────────────────────"