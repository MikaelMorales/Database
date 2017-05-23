<?php
ini_set("mysql.trace_mode", "0");
final class TablesInformations {
  private static $tableToAttributes = array(
    "Story" => ["title", "letters", "editing", "synopsis", "reprint_notes", "notes"],
    "Story_Artists" => ["name"],
    "Story_Characters" => ["name"],
    "Country" => ["code", "name"],
    "Brand_Group" => ["name", "notes", "url"],
    "Indicia_Publisher" => ["name", "notes", "url"],
    "Issue" => ["price", "page_count", "indicia_frequency", "notes", "isbn", "valid_isbn", "barcode", "title", "on_sale_date", "rating"],
    "Language" => ["code", "name"],
    "Publisher" => ["name", "notes", "url"],
    "Series" => ["name", "format", "notes", "dimensions", "publishing_format"],
    "Series_Publication_Type" => ["name"],
    "Story_Genres" => ["name"],
    "Story_Type" => ["name"]
  );

  private static $tableNamesToNicerNames = array(
    "Story" => "Story",
    "Story_Artists" => "Artists",
    "Story_Characters" => "Characters",
    "Country" => "Country",
    "Brand_Group" => "Brand Group",
    "Indicia_Publisher" => "Indicia Publisher",
    "Issue" => "Issue",
    "Language" => "Language",
    "Publisher" => "Publisher",
    "Series" => "Series",
    "Series_Publication_Type" => "Series Publication Type",
    "Story_Genres" => "Story Genre",
    "Story_Type" => "Story Type"
  );

  private static $idToName = array(
      1 => "Story",
      2 =>  "Story_Artists",
      3 => "Story_Characters",
      4 => "Country",
      5 => "Brand_Group",
      6 => "Indicia_Publisher",
      7 => "Issue",
      8 => "Language",
      9 => "Publisher",
      10 => "Series",
      11 => "Series_Publication_Type",
      12 => "Story_Genres",
      13 => "Story_Type"

  );

  private static $tables = array(
      "Story",
      "Story_Artists",
      "Story_Characters",
      "Country",
      "Brand_Group",
      "Indicia_Publisher",
      "Issue",
      "Language",
      "Publisher",
      "Series",
      "Series_Publication_Type",
      "Story_Genres",
      "Story_Type"
  );

private static $tablesToNumericAttributes = array(
    "Story" => ["id", "issue_id", "type_id"],
    "Story_Artists" => ["id"],
    "Story_Characters" => ["id"],
    "Country" => ["id"],
    "Brand_Group" => ["id", "publisher_id", "year_began", "year_ended"],
    "Indicia_Publisher" => ["id", "publisher_id", "country_id", "year_began", "year_ended"],
    "Issue" => ["id", "series_id", "indicia_publisher_id", "publication_date", "page_count", "on_sale_date"],
    "Language" => ["id"],
    "Publisher" => ["id", "country_id", "year_began", "year_ended"],
    "Series" => ["id", "year_began", "year_ended", "publication_dates", "first_issue_id", "last_issue_id", "publisher_id", "country_id", "language_id", "publication_type_id"],
    "Series_Publication_Type" => ["id"],
    "Story_Genres" => ["id"],
    "Story_Type" => ["id"]
);

private static $idToNameForClient = array(
    array("id" => "Story", "name" => "Story"),
    array("id" => "Story_Characters", "name" => "Characters"),
    array("id" => "Country", "name" => "Country"),
    array("id" => "Brand_Group", "name" => "Brand Group"),
    array("id" => "Indicia_Publisher", "name" => "Indicia Publisher"),
    array("id" => "Issue", "name" => "Issue"),
    array("id" => "Language", "name" => "Language"),
    array("id" => "Publisher", "name" => "Publisher"),
    array("id" => "Series", "name" => "Series"),
    array("id" => "Series_Publication_Type", "name" => "Series Publication Type"),
    array("id" => "Story_Genres", "name" => "Story Genre"),
    array("id" => "Story_Type", "name" => "Story Type")
);

  static function getAttributesOfTable($tableName) {
    return self::$tableToAttributes[$tableName];
  }

  static function getNicerNames($tableName) {
    return self::$tableNamesToNicerNames[$tableName];
  }

  static function getName($tableId) {
      return self::$idToName[$tableId];
  }

  static function getTables() {
      return self::$tables;
  }

  static function getNumericAttributes($tableName) {
      return self::$tablesToNumericAttributes[$tableName];
  }

  static function getIdToName() {
      return self::$idToNameForClient;
  }
}
?>
