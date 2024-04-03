#!/bin/bash

# Default values
dbname=""
username=""
password=""
port="5432"  # Default PostgreSQL port

# Function to display usage instructions
usage() {
    echo "Usage: $0 -d <dbname> -u <username> -p <password>"
    exit 1
}

# Parse command-line arguments
while getopts ":d:u:p:P:" opt; do
    case ${opt} in
        d)
            dbname=$OPTARG
            ;;
        u)
            username=$OPTARG
            ;;
        p)
            password=$OPTARG
            ;;
        \?)
            echo "Invalid option: $OPTARG"
            usage
            ;;
        :)
            echo "Option -$OPTARG requires an argument."
            usage
            ;;
    esac
done

# Check if required arguments are provided
if [[ -z $dbname || -z $username || -z $password ]]; then
    echo "Error: Required arguments missing."
    usage
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Installing..."
    sudo apt update
    sudo apt install postgresql postgresql-contrib
fi

# Start PostgreSQL service if not already running
if ! systemctl is-active --quiet postgresql; then
    echo "Starting PostgreSQL service..."
    sudo systemctl start postgresql
fi

# Create a new PostgreSQL database
echo "Creating a new database '$dbname' on port $port..."
sudo -u postgres psql -p $port -c "CREATE DATABASE $dbname;"

echo "Database '$dbname' created successfully."

# Create a new user with admin role
echo "Creating a new user '$username' with admin role..."
sudo -u postgres psql -p $port -c "CREATE USER $username WITH PASSWORD '$password';"
sudo -u postgres psql -p $port -c "ALTER USER $username WITH SUPERUSER;"

echo "User '$username' created with admin role."

# Provide additional instructions if needed
echo "PostgreSQL setup complete."

# Get host and port information from PostgreSQL configuration
host=$(sudo -u postgres psql -c "SHOW data_directory;" | sed -n 2p | cut -d' ' -f2)
port=$(sudo -u postgres psql -c "SHOW port;" | sed -n 2p | cut -d' ' -f2)

echo "PostgreSQL is running on host: $host and port: $port"

# Pause for 15 seconds
echo "Pausing for 15 seconds..."
sleep 15