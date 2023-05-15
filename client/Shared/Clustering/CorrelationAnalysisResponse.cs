using System.Text.Json.Serialization;

public class CorrelationAnalysisResponse
{
  
  [JsonPropertyName("map_filename")]
  public string MapFileName { get; set; }
  [JsonPropertyName("strong_corrs")]
  public List<List<string>> StrongCorrelations { get; set; }
}