using System.Text.Json.Serialization;

public class ClassificationExecutionResponse
{
  [JsonPropertyName("class_variable")]
  public string ClassVariable {get; set;}
  [JsonPropertyName("label")]
  public string Label {get; set;}
}