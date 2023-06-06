using System.Text.Json.Serialization;

public class PrognosisInfoResponse
{
  [JsonPropertyName("file_id")]
  public int Id {get; set;}
  [JsonPropertyName("criterio")]
  public string Criterio {get; set;}
  [JsonPropertyName("importance")]
  public Dictionary<string, float> Importance {get; set;}
  [JsonPropertyName("mean_absolute_error")]
  public float MeanAbsoluteError {get; set;}
  [JsonPropertyName("mean_squared_error")]
  public float MeanSquaredError {get; set;}
  [JsonPropertyName("root_mean_squared_error")]
  public float RootMeanSquaredError {get; set;}
  [JsonPropertyName("score")]
  public float Score {get; set;}
}