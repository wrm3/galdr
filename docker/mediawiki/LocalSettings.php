<?php
/**
 * LocalSettings.php — galdr MediaWiki
 * Auto-generated from environment variables. Do NOT edit manually.
 * To change settings, update your .env file and recreate the container.
 */

// ─── Core Identity ──────────────────────────────────────────────────────────
$wgSitename   = getenv('MEDIAWIKI_SITE_NAME')   ?: 'galdr Knowledge Base';
$wgMetaNamespace = 'Project';

// ─── Server & Paths ─────────────────────────────────────────────────────────
$wgServer    = rtrim(getenv('MEDIAWIKI_SERVER') ?: 'http://localhost:8880', '/');
$wgScriptPath = '';
$wgArticlePath = '/wiki/$1';
$wgUsePathInfo = true;

// ─── Database — PostgreSQL ───────────────────────────────────────────────────
$wgDBtype     = 'postgres';
$wgDBserver   = getenv('POSTGRES_HOST') ?: 'postgres';
$wgDBport     = getenv('POSTGRES_PORT') ?: '5432';
$wgDBname     = getenv('MEDIAWIKI_DB_NAME') ?: 'mediawiki';
$wgDBuser     = getenv('POSTGRES_USER') ?: 'galdr';
$wgDBpassword = getenv('POSTGRES_PASSWORD') ?: '';
$wgDBprefix   = getenv('MEDIAWIKI_DB_PREFIX') ?: 'mw_';
$wgDBssl      = false;

// ─── Security Keys (REQUIRED — generate with: openssl rand -hex 32) ─────────
$wgSecretKey   = getenv('MEDIAWIKI_SECRET_KEY')   ?: 'CHANGE_ME_generate_with_openssl_rand_hex_32';
$wgUpgradeKey  = getenv('MEDIAWIKI_UPGRADE_KEY')  ?: 'CHANGE_ME_generate_with_openssl_rand_hex_16';

// ─── Access Control ──────────────────────────────────────────────────────────
// Default: private wiki — only admins can read/write
$wgGroupPermissions['*']['read']              = false;
$wgGroupPermissions['*']['edit']              = false;
$wgGroupPermissions['*']['createaccount']     = false;
$wgGroupPermissions['user']['edit']           = true;
$wgGroupPermissions['user']['read']           = true;

// Override to public if env says so
if (strtolower(getenv('MEDIAWIKI_PUBLIC') ?: 'false') === 'true') {
    $wgGroupPermissions['*']['read']  = true;
    $wgGroupPermissions['*']['edit']  = false;  // read-only public
}

// ─── Email ───────────────────────────────────────────────────────────────────
$wgEnableEmail      = false;
$wgEnableUserEmail  = false;
$wgEmergencyContact = getenv('MEDIAWIKI_ADMIN_EMAIL') ?: 'admin@localhost';
$wgPasswordSender   = getenv('MEDIAWIKI_ADMIN_EMAIL') ?: 'admin@localhost';

// ─── Appearance ──────────────────────────────────────────────────────────────
$wgDefaultSkin = 'vector-2022';
wfLoadSkin('Vector');

// ─── Caching ─────────────────────────────────────────────────────────────────
$wgMainCacheType = CACHE_NONE;
$wgMessageCacheType = CACHE_NONE;
$wgParserCacheType  = CACHE_NONE;

// ─── Extensions ──────────────────────────────────────────────────────────────
wfLoadExtension('ParserFunctions');

// ─── Uploads ─────────────────────────────────────────────────────────────────
$wgEnableUploads  = false;   // Enable later if needed
$wgUseImageMagick = false;

// ─── Logo ─────────────────────────────────────────────────────────────────────
$wgLogos = [
    '1x'  => "$wgResourceBasePath/resources/assets/change-your-logo.svg",
    'icon' => "$wgResourceBasePath/resources/assets/change-your-logo.svg",
];

// ─── Misc ─────────────────────────────────────────────────────────────────────
$wgDiff3 = '/usr/bin/diff3';
$wgShellLocale = 'en_US.utf8';
$wgLanguageCode = 'en';
$wgRightsPage = '';
$wgRightsUrl  = '';
$wgRightsText = '';

// EOF
