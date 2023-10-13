use vision_db;
use admin;
db.createUser(
    {
        user: 'root',
        pwd: 'e61ddc9534f8efd85b6cd91a661fef9f',
        roles: [
            "UserAdminAnyDatabase",
            "dbAdminAnyDatabase",
            "readWriteAnyDatabase"
        ]
    }
)