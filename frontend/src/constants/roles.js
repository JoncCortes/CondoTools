export const ROLES = {
  PLATFORM_ADMIN: 'PLATFORM_ADMIN',
  SINDICO: 'SINDICO',
  PORTEIRO: 'PORTEIRO',
  MORADOR: 'MORADOR',
}

export const routePermissionMap = {
  '/dashboard': 'dashboard.view',
  '/units': 'units.view',
  '/residents': 'residents.view',
  '/visitors': 'visitors.view',
  '/visit-logs': 'visit_logs.view',
  '/packages': 'packages.view',
  '/announcements': 'announcements.view',
  '/incidents': 'occurrences.view',
  '/common-areas': 'common_areas.view',
  '/reservations': 'reservations.view',
  '/profile': 'profile.view',
  '/settings': 'settings.view',
}

export const staticMenuByRole = {
  [ROLES.PLATFORM_ADMIN]: ['/dashboard', '/units', '/residents', '/visitors', '/visit-logs', '/packages', '/announcements', '/incidents', '/common-areas', '/reservations', '/profile', '/settings'],
  [ROLES.SINDICO]: ['/dashboard', '/units', '/residents', '/visitors', '/visit-logs', '/packages', '/announcements', '/incidents', '/common-areas', '/reservations', '/profile'],
  [ROLES.PORTEIRO]: ['/dashboard', '/visitors', '/visit-logs', '/packages', '/profile'],
  [ROLES.MORADOR]: ['/dashboard', '/packages', '/announcements', '/incidents', '/reservations', '/profile'],
}
