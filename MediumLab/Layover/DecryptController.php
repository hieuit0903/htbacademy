<?php

namespace modules\htbairways\console\controllers;

use Craft;
use craft\db\Query;
use yii\console\Controller;
use yii\console\ExitCode;

class DecryptController extends Controller
{
    public function actionPassword(): int
    {
        $kv = array_column(
            (new Query())
                ->select(['name', 'value'])
                ->from('{{%htbairways_settings}}')
                ->all(),
            'value',
            'name'
        );

        $securityKey = Craft::$app->getConfig()->getGeneral()->securityKey;

        $encrypted = $kv['mailRelayPassword'];

        $password = Craft::$app->getSecurity()->decryptByKey(
            base64_decode($encrypted),
            $securityKey
        );

        $this->stdout("SMTP password: " . $password . PHP_EOL);

        return ExitCode::OK;
    }
}
