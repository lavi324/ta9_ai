# Question on the configure authenticate through AD:

### If we configure TA9 apps to authenticate with AD. What will happen to the local user?
(1) Will The existing local user be delete from the user table? **The existing local user will be disabled.**
(2) Will the existing local user still remain active and still able to login? **No.**
(3) Will the permission of the existing local user change? **No, because the existing local user will be disabled.**

### After configure to authenticate with AD:
(1) Can we still create new user (local and AD user) through admin studio? **No, you can’t create new user (local and AD user) through admin studio.**
(2) Can we still create new user (local and AD user) using User management API? **Yes, you can create new user (local and AD user) using User management API.**
(3) Can the rights and permission of the newly created user be configured through admin studio? Or API? Y**es for both, the rights and permission of the newly created user be configured through admin and API.**
(4) TA9 application will sync user list to TA9 user list? **Yes, TA9 application will sync user list to TA9 user list.**
(5) For newly sync in user, it is deactiviate by default? And what is their rights and permission? **New user is active, and can get default permission based on the configuration.**
(6) For newly sync in user, can the rights and permission be configured through admin studio? How about configure through API? **Yes, for both, the rights and permission be configured through admin studio and API.**
