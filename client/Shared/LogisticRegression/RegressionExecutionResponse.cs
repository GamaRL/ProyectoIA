using System.Text.Json.Serialization;

public class RegressionExecutionResponse
{
  [JsonPropertyName("label")]
  public string Label { get; set; }
  [JsonPropertyName("probability_0")]
  public float Probability0 { get; set; }
  [JsonPropertyName("probability_1")]
  public float Probability1 { get; set; }
}