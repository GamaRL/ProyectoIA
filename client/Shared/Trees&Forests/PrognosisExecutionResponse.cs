using System.Text.Json.Serialization;

public class PrognosisExecutionResponse
{
  [JsonPropertyName("prognosis_variable")]
  public string PrognosisVariable {get; set;}
  [JsonPropertyName("value")]
  public float Value {get; set;}
}