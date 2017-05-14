<?php
final class TablesInformations {
  private static $tableToAttributes = array(
    "Story" => ["title", "letters", "editing", "synopsis", "reprint_notes", "notes"],
    "Story_Artists" => ["name"],
    "Story_Characters" => ["name"]
  );

  private static $tableNamesToNicerNames = array(
    "Story" => "Story",
    "Story_Artists" => "Artists",
    "Story_Characters" => "Characters",
    "Brand_Group" => "Brand Group"
  );

  static function getAttributesOfTable($tableName) {
    return self::$tableToAttributes[$tableName];
  }

  static function getNicerNames($tableName) {
    return self::$tableNamesToNicerNames[$tableName];
  }

}
?>
