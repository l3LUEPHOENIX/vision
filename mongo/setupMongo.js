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
db.auth('root', 'e61ddc9534f8efd85b6cd91a661fef9f');
if (!db.auth('vision','a7c405c995052e2294c068292f6b0da6')) {
    db.createUser(
        {
            user: 'vision',
            pwd: 'a7c405c995052e2294c068292f6b0da6',
            roles: [
                {
                    role: 'readWrite',
                    db: 'vision_db'
                }
            ]
        }
    )
}