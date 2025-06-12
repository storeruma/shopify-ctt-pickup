<?php
require __DIR__ . '/vendor/autoload.php';
use GuzzleHttp\Client;

$clientId     = getenv('3DF9E0E9-3FFC-38FE-ADD1-55012AAD4C37');
$clientSecret = getenv('9F8AF421-DA10-3399-BCB0-53944941AFCE');

header('Content-Type: application/json');

$pc = $_GET['postal_code'] ?? '';
if (!$pc) {
  http_response_code(400);
  echo json_encode(['error' => 'postal_code missing']);
  exit;
}

try {
  $http = new Client([
    'base_uri' => 'https://enviosecommerceapi.ctt.pt/v3',
    'timeout'  => 5
  ]);

  $resp = $http->get("/pickup-points?postal_code={$pc}", [
    'headers' => [
      'X-IBM-Client-Id'     => $clientId,
      'X-IBM-Client-Secret' => $clientSecret
    ]
  ]);

  $j = json_decode($resp->getBody(), true);
  echo json_encode(['pickup_points' => $j['pickup_points'] ?? []]);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(['error' => $e->getMessage()]);
}
