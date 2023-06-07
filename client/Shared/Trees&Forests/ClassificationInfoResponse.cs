using System.Text.Json.Serialization;

public class ClassificationInfoResponse
{
  [JsonPropertyName("file_id")]
  public int FileId {get; set;}
  [JsonPropertyName("criterio")]
  public string Criterio {get; set;}
  [JsonPropertyName("importance")]
  public Dictionary<string, float> Importance {get; set;}
  [JsonPropertyName("score")]
  public float Score {get; set;}
  [JsonPropertyName("report")]
  public Dictionary<string, ReportRow> Report {get; set;}
  [JsonPropertyName("roc_image_file")]
  public string ROCImageFile {get; set;}
  [JsonPropertyName("crosstab")]
  public Dictionary<string, List<int>> CrossTab {get; set;}
}