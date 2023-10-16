use vision_db;
use admin;

if (!db.auth('root','e61ddc9534f8efd85b6cd91a661fef9f')) {
    db.createUser(
        {
            user: 'root',
            pwd: 'e61ddc9534f8efd85b6cd91a661fef9f',
            roles: [
                "userAdminAnyDatabase",
                "dbAdminAnyDatabase",
                "readWriteAnyDatabase"
            ]
        }
    )
}
