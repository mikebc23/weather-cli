class WeatherCli < Formula
  include Language::Python::Virtualenv

  desc "Fast, feature-rich command-line weather tool"
  homepage "https://github.com/mikebc23/weather-cli"
  url "https://files.pythonhosted.org/packages/source/c/cr-mb-weather-cli/cr_mb_weather_cli-1.0.0.tar.gz"
  sha256 "d35cacd01bc8220078946f5803863940d612188fccecff35fd73074022c249fc"
  license "MIT"

  depends_on "python@3.12"

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/source/u/urllib3/urllib3-2.0.4.tar.gz"
    sha256 "8d22f86aae8ef5e410d4f539fde9ce6b2113a001bb4d189e0aed70642d602b11"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    # Test that the binary exists and shows help
    assert_match "Simple command-line weather tool", shell_output("#{bin}/weather --help")
    
    # Test that it handles invalid input gracefully
    assert_match "Invalid date format", shell_output("#{bin}/weather --date invalid 2>&1", 1)
  end
end
