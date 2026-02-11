export const ROLES = {
  PLATFORM_ADMIN: 'PLATFORM_ADMIN',
  SINDICO: 'SINDICO',
  PORTEIRO: 'PORTEIRO',
  MORADOR: 'MORADOR',
}

export const pagePermissions = {
  '/dashboard': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.PORTEIRO, ROLES.MORADOR],
  '/units': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO],
  '/residents': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO],
  '/visitors': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.PORTEIRO],
  '/visit-logs': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.PORTEIRO],
  '/packages': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.PORTEIRO, ROLES.MORADOR],
  '/announcements': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.MORADOR],
  '/incidents': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.MORADOR],
  '/common-areas': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.MORADOR],
  '/reservations': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.MORADOR],
  '/profile': [ROLES.PLATFORM_ADMIN, ROLES.SINDICO, ROLES.PORTEIRO, ROLES.MORADOR],
}

export const menuByRole = {
  [ROLES.PLATFORM_ADMIN]: ['/dashboard', '/units', '/residents', '/visitors', '/visit-logs', '/packages', '/announcements', '/incidents', '/common-areas', '/reservations', '/profile'],
  [ROLES.SINDICO]: ['/dashboard', '/units', '/residents', '/visitors', '/visit-logs', '/packages', '/announcements', '/incidents', '/common-areas', '/reservations', '/profile'],
  [ROLES.PORTEIRO]: ['/dashboard', '/visitors', '/visit-logs', '/packages', '/profile'],
  [ROLES.MORADOR]: ['/dashboard', '/packages', '/announcements', '/incidents', '/reservations', '/profile'],
}
