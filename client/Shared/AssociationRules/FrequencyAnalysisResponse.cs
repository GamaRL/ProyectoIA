using System.Text.Json.Serialization;

public class FrequencyAnalysisResponse
{
  [JsonPropertyName("item")]
  public string Item { get; set; }
  [JsonPropertyName("frequency")]
  public int Frequency { get; set; }
  [JsonPropertyName("relative")]
  public float Relative { get; set;}
}