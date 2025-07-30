# psycopg2-binary Installation Fixes

## Quick Fix Options (Try in order)

### Option 1: Install system dependencies first
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libpq-dev python3-dev build-essential

# On CentOS/RHEL/Fedora
sudo yum install -y postgresql-devel python3-devel gcc

# On macOS
brew install postgresql
```

### Option 2: Use pre-compiled wheel (Recommended)
```bash
pip install --only-binary=psycopg2-binary psycopg2-binary==2.9.10
```

### Option 3: Try different version
```bash
pip install psycopg2-binary==2.9.7
```

### Option 4: Use asyncpg instead (Modern alternative)
```bash
# Replace psycopg2-binary with asyncpg in requirements.txt
pip install asyncpg==0.29.0
```

### Option 5: Force binary installation
```bash
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir psycopg2-binary
```

### Option 6: Use pip with constraints
```bash
pip install psycopg2-binary --prefer-binary --no-build-isolation
```

## For Docker Development

If you're using Docker (recommended), the installation should work automatically. Use:

```bash
docker compose up --build
```

This bypasses local Python environment issues.

## Alternative: Use the provided requirements-alternative.txt

```bash
pip install -r requirements-alternative.txt
```

This uses `asyncpg` instead of `psycopg2-binary`, which is often easier to install and more performant.

## Database URL Changes for asyncpg

If using asyncpg, update your DATABASE_URL format:
```bash
# From psycopg2 format:
DATABASE_URL=postgresql://user:password@localhost/database

# To asyncpg format:
DATABASE_URL=postgresql+asyncpg://user:password@localhost/database
```