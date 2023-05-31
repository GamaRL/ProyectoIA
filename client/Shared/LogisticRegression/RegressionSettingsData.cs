using System.Text.Json.Serialization;

public class RegressionSettingsData
{
  [JsonPropertyName("id")]
  public int Id {get; set;}
  [JsonPropertyName("file_id")]
  public int FileId {get; set;}
  [JsonPropertyName("contains_headers")]
  public bool ContainsHeaders {get; set;}
  [JsonPropertyName("predictor_variables")]
  public List<object> PredictorVariables {get; set;}
  [JsonPropertyName("class_variable")]
  public object ClassVariable {get; set;}
  [JsonPropertyName("test_size")]
  public float TestSize {get; set;}
  [JsonPropertyName("shuffle")]
  public bool Shuffle {get; set;}
}