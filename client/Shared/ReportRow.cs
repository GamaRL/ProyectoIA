using System.Text.Json.Serialization;

public class ReportRow
{
  [JsonPropertyName("precision")]
  public float Precision {get; set;}
  [JsonPropertyName("recall")]
  public float Recall {get; set;}
  [JsonPropertyName("f1-score")]
  public float F1Score {get; set;}
  [JsonPropertyName("support")]
  public float Support {get; set;}
}