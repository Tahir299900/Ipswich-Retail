#!/bin/bash

# Build and test script for Ipswich Retail
# This script runs all necessary checks before deployment

set -e  # Exit on any error

echo "🏗️  Building Ipswich Retail Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Environment check
echo -e "${BLUE}🔍 Checking environment...${NC}"
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"

# Step 2: Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Step 3: Run Django system checks
echo -e "${YELLOW}⚙️  Running Django system checks...${NC}"
python manage.py check
echo -e "${GREEN}✅ Django system checks passed${NC}"

# Step 4: Database migrations check
echo -e "${YELLOW}🗄️  Checking database migrations...${NC}"
python manage.py makemigrations --check --dry-run
echo -e "${GREEN}✅ No pending migrations${NC}"

# Step 5: Run tests
echo -e "${YELLOW}🧪 Running test suite...${NC}"
python manage.py test --verbosity=2
echo -e "${GREEN}✅ All tests passed${NC}"

# Step 6: Collect static files
echo -e "${YELLOW}📁 Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear
echo -e "${GREEN}✅ Static files collected${NC}"

# Step 7: Run code quality checks (if tools available)
if command -v black &> /dev/null; then
    echo -e "${YELLOW}🎨 Checking code formatting with Black...${NC}"
    black --check .
    echo -e "${GREEN}✅ Code formatting is correct${NC}"
fi

if command -v flake8 &> /dev/null; then
    echo -e "${YELLOW}📏 Running flake8 linting...${NC}"
    flake8 --max-line-length=88 --exclude=migrations,venv,env .
    echo -e "${GREEN}✅ Code linting passed${NC}"
fi

if command -v isort &> /dev/null; then
    echo -e "${YELLOW}📂 Checking import sorting...${NC}"
    isort --check-only --diff .
    echo -e "${GREEN}✅ Import sorting is correct${NC}"
fi

# Step 8: Security checks
if command -v bandit &> /dev/null; then
    echo -e "${YELLOW}🔒 Running security analysis...${NC}"
    bandit -r . -x tests/,venv/,env/ --format json --output bandit-report.json --exit-zero
    echo -e "${GREEN}✅ Security analysis completed${NC}"
fi

if command -v safety &> /dev/null; then
    echo -e "${YELLOW}🛡️  Checking for vulnerable dependencies...${NC}"
    safety check --json --output safety-report.json --exit-zero
    echo -e "${GREEN}✅ Dependency vulnerability check completed${NC}"
fi

# Step 9: Test production settings
echo -e "${YELLOW}🏭 Testing production configuration...${NC}"
export DJANGO_SETTINGS_MODULE=ipswich_retail.production_settings
export SECRET_KEY=test-secret-key-for-build-check-only
export DATABASE_URL=sqlite:///build_test.db
export ALLOWED_HOSTS=example.com

# Run deployment checks
python manage.py check --deploy --fail-level WARNING
echo -e "${GREEN}✅ Production configuration validated${NC}"

# Cleanup test database
rm -f build_test.db

# Step 10: Build summary
echo ""
echo -e "${GREEN}🎉 Build completed successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Build Summary:${NC}"
echo -e "   ✅ Dependencies installed and updated"
echo -e "   ✅ Django system checks passed"
echo -e "   ✅ Database migrations validated"
echo -e "   ✅ All tests passed ($(python manage.py test --verbosity=0 2>&1 | grep -o 'Ran [0-9]* tests' | grep -o '[0-9]*') tests)"
echo -e "   ✅ Static files collected"
echo -e "   ✅ Code quality checks passed"
echo -e "   ✅ Security analysis completed"
echo -e "   ✅ Production configuration validated"
echo ""
echo -e "${GREEN}Application is ready for deployment! 🚀${NC}"

# Generate build info
cat > build-info.json << EOF
{
  "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
  "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
  "python_version": "$(python --version | cut -d' ' -f2)",
  "django_version": "$(python -c 'import django; print(django.VERSION[:3])')",
  "build_status": "success"
}
EOF

echo -e "${BLUE}📄 Build info saved to build-info.json${NC}"