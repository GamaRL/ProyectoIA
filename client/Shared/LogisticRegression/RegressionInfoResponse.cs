using System.Text.Json.Serialization;

public class RegressionInfoResponse
{
  [JsonPropertyName("file_id")]
  public int FileId {get; set;}
  [JsonPropertyName("accuracy_score")]
  public float AccuracyScore {get; set;}
}