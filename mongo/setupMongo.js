const admin_user = process.env.MONGO_ADMIN_USER
const user_user = process.env.MONGO_USER_USER
const admin_pass = process.env.MONGO_ADMIN_PASS
const user_pass = process.env.MONGO_USER_PASS

use admin;
if (!db.auth(admin_user, admin_pass)) {
    db.createUser(
        {
            user: admin_user,
            pwd: admin_pass,
            roles: [
                "userAdminAnyDatabase",
                "dbAdminAnyDatabase",
                "readWriteAnyDatabase"
            ]
        }
    )
}
use vision_db;
if (!db.auth(user_user, user_pass)) {
    db.createUser(
        {
            user: user_user,
            pwd: user_pass,
            roles: [
                {
                    role: 'readWrite',
                    db: 'vision_db'
                }
            ]
        }
    )
}