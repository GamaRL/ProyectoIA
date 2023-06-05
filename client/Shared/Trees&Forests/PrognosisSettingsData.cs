using System.Text.Json.Serialization;

public class PrognosisSettingsData
{
  [JsonPropertyName("id")]
  public int Id {get; set;}
  [JsonPropertyName("file_id")]
  public int FileId {get; set;}
  [JsonPropertyName("contains_headers")]
  public bool ContainsHeaders {get; set;}
  [JsonPropertyName("predictor_variables")]
  public List<object> PredictorVariables {get; set;}
  [JsonPropertyName("prognosis_variable")]
  public string PrognosisVariable {get; set;}
  [JsonPropertyName("test_size")]
  public float TestSize {get; set;}
  [JsonPropertyName("shuffle")]
  public bool Shuffle {get; set;}
  [JsonPropertyName("use_forest")]
  public bool UseForest {get; set;}
  [JsonPropertyName("n_estimators")]
  public int NEstimators {get; set;}
  [JsonPropertyName("max_depth")]
  public int MaxDepth {get; set;}
  [JsonPropertyName("min_samples_split")]
  public int MinSamplesSplit {get; set;}
  [JsonPropertyName("min_samples_leaf")]
  public int MinSamplesLeaf {get; set;}
}