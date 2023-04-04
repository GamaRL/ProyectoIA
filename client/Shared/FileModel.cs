using System.Text.Json.Serialization;

public class FileModel
{
  [JsonPropertyName("id")]
  public int Id { get; set; }
  [JsonPropertyName("name")]
  public string Name { get; set; }
  [JsonPropertyName("file_token")]
  public string FileToken { get; set; }
  [JsonPropertyName("algorithm")]
  public AlgorithmType Algorithm { get; set; }
}