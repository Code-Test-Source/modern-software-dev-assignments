#!/usr/bin/env zsh

echo "=========================================="
echo "Weather MCP Server Test Suite"
echo "=========================================="

# Configuration
PORT=8770
API_KEY="test-secret-key"
BASE_URL="http://localhost:$PORT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

pass() { echo -e "${GREEN}✓ PASS${NC}: $1"; ((TESTS_PASSED++)); }
fail() { echo -e "${RED}✗ FAIL${NC}: $1"; ((TESTS_FAILED++)); }
info() { echo -e "${YELLOW}ℹ INFO${NC}: $1"; }

cleanup() {
    pkill -f "server.main.*$PORT" 2>/dev/null || true
    pkill -f "server.main.*8771" 2>/dev/null || true
}
trap cleanup EXIT

info "Starting HTTP server with authentication..."
WEATHER_API_KEY=$API_KEY python -m server.main --mode http --port $PORT &
sleep 3

echo ""
echo "=========================================="
echo "Running Tests"
echo "=========================================="
echo ""

# Test 1: Health without auth
info "Test 1: Health check without authentication"
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/t1.txt "$BASE_URL/health")
if [ "$RESPONSE" = "401" ]; then
    pass "Health check requires auth"
else
    fail "Expected 401, got $RESPONSE"
fi

# Test 2: Health with valid auth
info "Test 2: Health check with valid authentication"
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/t2.txt -H "Authorization: Bearer $API_KEY" "$BASE_URL/health")
if [ "$RESPONSE" = "200" ]; then
    pass "Health check succeeds with valid key"
else
    fail "Expected 200, got $RESPONSE"
fi

# Test 3: Health with invalid auth
info "Test 3: Health check with invalid authentication"
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/t3.txt -H "Authorization: Bearer wrong" "$BASE_URL/health")
if [ "$RESPONSE" = "401" ]; then
    pass "Health check rejects invalid key"
else
    fail "Expected 401, got $RESPONSE"
fi

# Test 4: Rate limiting
info "Test 4: Rate limiting (100 requests per minute)"
RATE_HIT=false
for i in {1..105}; do
    RESP=$(curl -s -w "%{http_code}" -o /dev/null -H "Authorization: Bearer $API_KEY" "$BASE_URL/health")
    if [ "$RESP" = "429" ]; then
        RATE_HIT=true
        pass "Rate limit triggered at request $i"
        break
    fi
done
if [ "$RATE_HIT" = false ]; then
    fail "Rate limiting did not trigger"
fi

# Test 5: Server without API key
info "Test 5: Server starts without API key"
pkill -f "server.main.*$PORT" 2>/dev/null
sleep 1
PORT2=8771
$CONDA_RUN python -m server.main --mode http --port $PORT2 &
sleep 2
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/t5.txt "http://localhost:$PORT2/health")
if [ "$RESPONSE" = "200" ]; then
    pass "Server works without API_KEY"
else
    fail "Expected 200, got $RESPONSE"
fi
pkill -f "server.main.*$PORT2" 2>/dev/null
sleep 1

# Test 6: STDIO mode
info "Test 6: STDIO mode starts"
OUTPUT=$(timeout 2 $CONDA_RUN python -m server.main --mode stdio 2>&1 || true)
if echo "$OUTPUT" | grep -q "Starting Weather MCP Server"; then
    pass "STDIO mode starts"
else
    fail "STDIO mode failed"
fi

# Test 7: City validation - empty
info "Test 7: City validation - empty city"
OUTPUT=$($CONDA_RUN python -c "from server.main import _validate_city; _validate_city('')" 2>&1)
if echo "$OUTPUT" | grep -q "required"; then
    pass "Empty city rejected"
else
    fail "Empty city validation failed"
fi

# Test 8: City validation - too short
info "Test 8: City validation - too short"
OUTPUT=$($CONDA_RUN python -c "from server.main import _validate_city; _validate_city('A')" 2>&1)
if echo "$OUTPUT" | grep -q "at least 2"; then
    pass "Short city rejected"
else
    fail "Short city validation failed"
fi

# Test 9: Days validation - too many
info "Test 9: Days validation - > 7"
OUTPUT=$($CONDA_RUN python -c "from server.main import _validate_days; _validate_days(10)" 2>&1)
if echo "$OUTPUT" | grep -q "at most 7"; then
    pass "Days > 7 rejected"
else
    fail "Days validation failed"
fi

# Test 10: Days validation - invalid type
info "Test 10: Days validation - invalid type"
OUTPUT=$($CONDA_RUN python -c "from server.main import _validate_days; _validate_days('abc')" 2>&1)
if echo "$OUTPUT" | grep -q "integer"; then
    pass "Non-integer days rejected"
else
    fail "Days type validation failed"
fi

# Test 11: Tools exist
info "Test 11: Tool definitions"
OUTPUT=$($CONDA_RUN python -c "import asyncio; from server.main import list_tools; t=asyncio.run(list_tools()); print([x.name for x in t])" 2>&1)
if echo "$OUTPUT" | grep -q "get_current_weather"; then
    pass "get_current_weather tool exists"
else
    fail "Tool missing"
fi
if echo "$OUTPUT" | grep -q "get_weather_forecast"; then
    pass "get_weather_forecast tool exists"
else
    fail "Tool missing"
fi

# Test 12: Invalid city error handling
info "Test 12: Error handling - invalid city"
OUTPUT=$($CONDA_RUN python -c "import asyncio; from server.main import call_tool; r=asyncio.run(call_tool('get_current_weather', {'city': 'InvalidCityXYZ123'})); print(r[0].text)" 2>&1)
if echo "$OUTPUT" | grep -q -E "Error|not found"; then
    pass "Invalid city returns error"
else
    fail "Error handling failed"
fi

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
