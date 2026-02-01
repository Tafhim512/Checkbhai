#!/bin/bash

# CheckBhai Pre-Deployment Readiness Check Script
# Run this before deploying to verify all files are ready

echo "🔍 CheckBhai Pre-Deployment Readiness Check"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0
warnings=0

# Check if we're in the right directory
if [ ! -d "checkbhai-backend" ] || [ ! -d "checkbhai-frontend" ]; then
    echo -e "${RED}❌ Error: Must run from CheckBhai root directory${NC}"
    exit 1
fi

echo "📂 Checking project structure..."

# Check backend files
echo ""
echo "Backend Files:"
files=(
    "checkbhai-backend/app/main.py"
    "checkbhai-backend/app/database.py"
    "checkbhai-backend/app/auth.py"
    "checkbhai-backend/app/ai_engine.py"
    "checkbhai-backend/app/rules_engine.py"
    "checkbhai-backend/app/training_data.py"
    "checkbhai-backend/requirements.txt"
    "checkbhai-backend/Dockerfile"
    "checkbhai-backend/.env.example"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗ Missing: $file${NC}"
        ((errors++))
    fi
done

# Check routers
echo ""
echo "Backend Routers:"
routers=(
    "checkbhai-backend/app/routers/auth.py"
    "checkbhai-backend/app/routers/check.py"
    "checkbhai-backend/app/routers/history.py"
    "checkbhai-backend/app/routers/payment.py"
    "checkbhai-backend/app/routers/admin.py"
)

for router in "${routers[@]}"; do
    if [ -f "$router" ]; then
        echo -e "${GREEN}✓${NC} $router"
    else
        echo -e "${RED}✗ Missing: $router${NC}"
        ((errors++))
    fi
done

# Check frontend files
echo ""
echo "Frontend Files:"
frontend_files=(
    "checkbhai-frontend/app/layout.tsx"
    "checkbhai-frontend/app/page.tsx"
    "checkbhai-frontend/app/globals.css"
    "checkbhai-frontend/app/history/page.tsx"
    "checkbhai-frontend/app/payment/page.tsx"
    "checkbhai-frontend/app/admin/page.tsx"
    "checkbhai-frontend/package.json"
    "checkbhai-frontend/tailwind.config.ts"
    "checkbhai-frontend/.env.local.example"
)

for file in "${frontend_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗ Missing: $file${NC}"
        ((errors++))
    fi
done

# Check components
echo ""
echo "Frontend Components:"
components=(
    "checkbhai-frontend/components/CheckBhaiAvatar.tsx"
    "checkbhai-frontend/components/RiskBadge.tsx"
    "checkbhai-frontend/components/RedFlagsList.tsx"
)

for component in "${components[@]}"; do
    if [ -f "$component" ]; then
        echo -e "${GREEN}✓${NC} $component"
    else
        echo -e "${RED}✗ Missing: $component${NC}"
        ((errors++))
    fi
done

# Check API client
if [ -f "checkbhai-frontend/lib/api.ts" ]; then
    echo -e "${GREEN}✓${NC} checkbhai-frontend/lib/api.ts"
else
    echo -e "${RED}✗ Missing: checkbhai-frontend/lib/api.ts${NC}"
    ((errors++))
fi

# Check deployment configs
echo ""
echo "Deployment Configuration:"
configs=(
    "vercel.json"
    "railway.json"
    "README.md"
    ".gitignore"
)

for config in "${configs[@]}"; do
    if [ -f "$config" ]; then
        echo -e "${GREEN}✓${NC} $config"
    else
        echo -e "${YELLOW}⚠${NC} Missing: $config (optional but recommended)"
        ((warnings++))
    fi
done

# Check for sensitive files
echo ""
echo "Security Check:"
if [ -f "checkbhai-backend/.env" ]; then
    echo -e "${YELLOW}⚠ Warning: .env file found - ensure it's in .gitignore${NC}"
    ((warnings++))
else
    echo -e "${GREEN}✓${NC} No .env files committed"
fi

if [ -f "checkbhai-frontend/.env.local" ]; then
    echo -e "${YELLOW}⚠ Warning: .env.local file found - ensure it's in .gitignore${NC}"
    ((warnings++))
else
    echo -e "${GREEN}✓${NC} No .env.local files committed"
fi

# Check training data
echo ""
echo "AI Training Data Check:"
if grep -q "TRAINING_DATA = \[" checkbhai-backend/app/training_data.py 2>/dev/null; then
    count=$(grep -c '"text":' checkbhai-backend/app/training_data.py 2>/dev/null || echo "0")
    if [ "$count" -ge 50 ]; then
        echo -e "${GREEN}✓${NC} Training data contains $count examples (>= 50 required)"
    else
        echo -e "${RED}✗ Training data only has $count examples (need >= 50)${NC}"
        ((errors++))
    fi
else
    echo -e "${RED}✗ Training data file invalid or missing${NC}"
    ((errors++))
fi

# Summary
echo ""
echo "=========================================="
echo "Summary:"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Push to GitHub: git push origin main"
    echo "2. Follow DEPLOYMENT_CHECKLIST.md"
    echo "3. Deploy backend to Railway/Render"
    echo "4. Deploy frontend to Vercel"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠ $warnings warning(s) found${NC}"
    echo -e "${GREEN}✓ No critical errors - can proceed with deployment${NC}"
    echo ""
    echo "Review warnings above and fix if necessary"
    exit 0
else
    echo -e "${RED}❌ $errors error(s) found${NC}"
    if [ $warnings -gt 0 ]; then
        echo -e "${YELLOW}⚠ $warnings warning(s) found${NC}"
    fi
    echo ""
    echo "Please fix errors before deploying"
    exit 1
fi
