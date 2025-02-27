using System.Text.Json.Serialization;

public class RegressionInfoResponse
{
  [JsonPropertyName("file_id")]
  public int FileId {get; set;}
  [JsonPropertyName("accuracy_score")]
  public float AccuracyScore {get; set;}
  [JsonPropertyName("report")]
  public Dictionary<string, ReportRow> Report {get; set;}
  [JsonPropertyName("roc_image_file")]
  public string ROCImageFile {get; set;}
  [JsonPropertyName("crosstab")]
  public Dictionary<string, List<int>> CrossTab {get; set;}
}